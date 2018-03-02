/*
 *  Created on: Mar 01, 2018
 *  Created by: Huu Nghia NGUYEN <huunghia.nguyen@montimage.com>
 */
#include <stdio.h>
#include <signal.h>
#include <stdbool.h>
#include <stdlib.h> // size_t
#include <inttypes.h> //PRIu16
#include <string.h>
#include <limits.h>
#include <execinfo.h>
#include <sys/types.h>
#include <unistd.h>
#include <locale.h>

#define true  1
#define false 0

struct point{
	uint16_t row;
	uint16_t col;
};

struct vehicule{
	struct point pos;
	size_t step;
	uint16_t *rides;
	uint16_t nb_rides;
} **vehicules;

struct ride{
	struct point start_pos;
	struct point end_pos;
	uint16_t distance; //distance from start -> end
	size_t early_step;
	size_t final_step;
	uint16_t id;
} **rides;

struct{
	uint16_t nb_rows;
	uint16_t nb_cols;
	uint16_t nb_vehicules;
	uint16_t nb_rides;
	uint16_t bonus;
	size_t steps;
}input;


#define DISTANCE( a, b ) (a>b? a-b : b-a )

static inline uint16_t distance( const struct point *a, const struct point *b ){
	return (DISTANCE( a->col, b->col ) + DISTANCE( a->row, b->row ));
}


size_t total_score = 0;
size_t total_vehicule = 0;
uint32_t **best_scores_table;

void read_data( const char *file_name){
	int i;
	char c;

	FILE *file = fopen( file_name, "r" );
	if( file == NULL ){
		fprintf(stderr, "Error: cannot find file %s", file_name );
		exit( 1 );
	}

	fscanf( file, "%"SCNd16, &input.nb_rows );
	fscanf( file, "%"SCNd16, &input.nb_cols );
	fscanf( file, "%"SCNd16, &input.nb_vehicules );
	fscanf( file, "%"SCNd16, &input.nb_rides );
	fscanf( file, "%"SCNd16, &input.bonus );
	fscanf( file, "%zu", &input.steps );


	rides     = malloc( sizeof( void * ) * input.nb_rides );

	//read new line
	fscanf( file, "%c", &c );

	//read matrix
	for( i=0; i<input.nb_rides; i++ ){
		rides[i] = malloc( sizeof( struct ride ));
		struct ride *r = rides[i];

		fscanf( file, "%"SCNd16, &r->start_pos.row );
		fscanf( file, "%"SCNd16, &r->start_pos.col );
		fscanf( file, "%"SCNd16, &r->end_pos.row );
		fscanf( file, "%"SCNd16, &r->end_pos.col );
		fscanf( file, "%zu",     &r->early_step );
		fscanf( file, "%zu",     &r->final_step );
		//read new line
		fscanf( file, "%c", &c );

		r->id = i;
		r->distance = distance( &r->start_pos, &r->end_pos );
	}

	//initialize vehicles
	total_vehicule = input.nb_vehicules;
	vehicules = malloc( sizeof( void* ) * total_vehicule );
	best_scores_table = malloc( sizeof( void* ) * total_vehicule );
	for( i=0; i<input.nb_vehicules; i++ ){
		best_scores_table[i] = malloc( sizeof( size_t ) * input.nb_rides );
		vehicules[i] = malloc( sizeof( struct vehicule ));
		vehicules[i]->nb_rides = 0;
		vehicules[i]->pos.col  = 0;
		vehicules[i]->pos.row  = 0;
		vehicules[i]->step     = 0;
		vehicules[i]->rides    = malloc( sizeof( uint16_t ) * input.nb_rides );
	}
}


void print_result(){
	int i, j;
	char file_name[1000];

	//open file: hashcode-score-pid.txt
	snprintf( file_name, sizeof( file_name ), "/media/sf_share_vbox/hashcode-%09zu-%05d.txt", total_score,  getpid() );
	FILE *file = fopen( file_name, "w" );
	if( file == NULL ){
		fprintf(stderr, "Error: cannot find file %s", file_name );
		exit( 1 );
	}

	struct vehicule *v;
	//write result
	for( i=0; i<total_vehicule; i++ ){
		v = vehicules[i];
		fprintf(file, "%d", v->nb_rides);
		for( j=0; j<v->nb_rides; j++ )
			fprintf( file, " %d", v->rides[j] );
		fprintf(file, "\n" );
	}

	setlocale( LC_NUMERIC, "en_US.UTF-8" );
	printf("total score: %'zu\n", total_score );
}

static inline size_t calcul_score( const struct vehicule *v, const struct ride *r ){
	//smallest score to win if riding
	uint32_t score = r->distance;

	//nb of steps to goto starting point
	uint32_t first = distance( &v->pos, &r->start_pos );

	size_t step_at_arrival = v->step + first;
	//vehicle needs to wait for its client
	if( step_at_arrival <= r->early_step ){
		step_at_arrival = r->early_step;
		score  += input.bonus*3; //client does not need to wait its taxi
	}

	//
	if( first > score && score > 20 )
		score -= 20;

	//vehicle arrives late: missed
	size_t step_after_riding = step_at_arrival + r->distance;
	if( step_after_riding > r->final_step //not arrival at time
			|| step_after_riding >= input.steps //outside of simulation
		)
		return 0;

	//if there exist another ride after this ride
	int i;
	struct ride *ri;
	size_t d;
	for( i=0; i<input.nb_rides; i++ ){
		ri = rides[i];

		//move to this ride
		d = distance( &r->end_pos, & ri->start_pos );

		//cat not arrive at time
		if( ri->final_step > r->final_step + ri->distance + d)
			continue;

		if( ri->early_step >= r->final_step + d )
			score += input.bonus;

		score += ri->distance;
	}


	return score;
}


static inline void select_vehicule_ride(  ){
	int i, j;
	//all rides are finished
	if( input.nb_rides == 0 || input.nb_vehicules == 0 )
		return;

	int best_ride = 0;
	int best_vehicule = 0;

	uint32_t max_score = best_scores_table[0][0];
	//each vehicule
	for( i=0; i<input.nb_vehicules; i++  ){
		for( j=0; j<input.nb_rides; j++ ){
			if( best_scores_table[i][j] > max_score ){

				max_score = best_scores_table[i][j];
				best_vehicule  = i;
				best_ride      = j;
			}
		}
	}
	if( max_score == 0 )
		return;

//	//assign the best_ride to the best_vehicule
	struct vehicule *v = vehicules[ best_vehicule ];
	struct ride     *r = rides[ best_ride ];

	total_score += r->distance;

	v->rides[ vehicules[ best_vehicule ]->nb_rides ] = r->id;
	v->nb_rides ++;

	//update clock of this vehicle
	v->step += distance( &v->pos, &r->start_pos ); //move to starting point
	if( v->step < r->early_step ){ //need to wait for its client ???
		v->step      = r->early_step; //move to end point
		total_score += input.bonus;   //bonus as its client does not need to wait
	}
	v->step += r->distance;

	//update new position of this vehicle
	v->pos.col = r->end_pos.col;
	v->pos.row = r->end_pos.row;

	//remove the performed ride by swapping it with the last ride
	input.nb_rides --;
	rides[ best_ride ] = rides[ input.nb_rides ];

	//update score of the new one
	for( i=0; i<input.nb_vehicules; i++ )
		best_scores_table[ i ][ best_ride ] = best_scores_table[ i ][ input.nb_rides ];


	//remove the vehicle if it is out of date
	if( vehicules[ best_vehicule ]->step >= input.steps ){

		input.nb_vehicules --;
		vehicules[ best_vehicule ] = vehicules[ input.nb_vehicules ];


		//update score
		for( j=0; j<input.nb_rides; j++ )
			best_scores_table[ best_vehicule ][ j ] = best_scores_table[ input.nb_vehicules ][ j ];
		return;
	}

	//update best_score after the best_vehicule performing its ride
	for( j=0; j<input.nb_rides; j++ )
		best_scores_table[ best_vehicule ][ j ] = calcul_score( vehicules[ best_vehicule ], rides[ j ] );

	//next round
	select_vehicule_ride();
}


/* Obtain a backtrace */
void print_execution_trace () {
	void *array[10];
	size_t size;
	char **strings;
	size_t i;
	size    = backtrace (array, 10);
	strings = backtrace_symbols (array, size);

	//i=2: ignore 2 first elements in trace as they are: this fun, then mmt_log
	for (i = 2; i < size; i++)
		printf( "%zu. %s\n", (i-1), strings[i]);

	free (strings);
	fflush( stdout );
}

void signal_handler( int sig ){
	print_result();
	print_execution_trace();
	exit( 1 );
}


int main( int argc, char **argv){
	int i,j;
	if( argc != 2 ){
		fprintf(stderr, "Usage: %s file_name\n", argv[0] );
		exit( 1 );
	}

	signal(SIGINT,  signal_handler);
	signal(SIGTERM, signal_handler);

	read_data( argv[1] );

	for( i=0; i<input.nb_vehicules; i++ )
		for( j=0; j<input.nb_rides; j++ ){
			best_scores_table[i][j] = calcul_score( vehicules[i], rides[j] );
		}

	select_vehicule_ride();

	print_result();

	return 0;
}

