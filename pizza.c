/*
 *  Created on: Mar 01, 2018
 *  Created by: Huu Nghia NGUYEN <huunghia.nguyen@montimage.com>
 */
#include <stdio.h>
#include <signal.h>
#include <stdlib.h> // size_t
#include <inttypes.h> //PRIu16
#include <string.h>
#include <limits.h>
#include <execinfo.h>
#include <sys/types.h>
#include <unistd.h>

static struct pizza_struct{
	uint16_t rows;
	uint16_t columns;
	uint16_t min_ingredient;
	uint16_t max_cells;
	uint8_t data[1000][1000]; //each
										//cell=1 if it contains tomato otherwise
										//cell=0 if it contains mushroom
}pizza;

void read_data( const char *file_name){
	int i,j;
	char c;

	FILE *file = fopen( file_name, "r" );
	if( file == NULL ){
		fprintf(stderr, "Error: cannot find file %s", file_name );
		exit( 1 );
	}

	fscanf( file, "%"SCNd16, &pizza.rows );
	fscanf( file, "%"SCNd16, &pizza.columns );
	fscanf( file, "%"SCNd16, &pizza.min_ingredient );
	fscanf( file, "%"SCNd16, &pizza.max_cells );

	//read new line
	fscanf( file, "%c", &c );

	//read matrix
	for( i=0; i<pizza.rows; i++ ){
		for( j=0; j<pizza.columns; j++ ){
			fscanf( file, "%c", &c );
			if( c == 'T')
				pizza.data[i][j] = 1;
			else if( c == 'M' )
				pizza.data[i][j] = 0;
			else
				printf("Error %d %d: %c\n", i, j, c);
		}
		//read new line
		fscanf( file, "%c", &c );
	}
}


void print_data(){
	size_t i, j;
	printf("%d %d %d %d\n", pizza.rows, pizza.columns, pizza.min_ingredient, pizza.max_cells );
	for( i=0; i<pizza.rows; i++ ){
			for( j=0; j<pizza.columns; j++ )
				printf("%c", (pizza.data[i][j] ? 'T' : 'M') );

			printf("\n");
	}
}


typedef struct slices_struct{
	uint16_t total_cells;
	uint16_t length;

	uint16_t row1[1000*1000];
	uint16_t col1[1000*1000];
	uint16_t row2[1000*1000];
	uint16_t col2[1000*1000];
}slices_t;

slices_t result;
void print_result(){
	size_t i;
	const slices_t* s = &result;
	size_t score;
	char file_name[1000];

	score = s->total_cells;

	//open file: hashcode-score-pid.txt
	snprintf( file_name, sizeof( file_name ), "/tmp/hashcode-%09zu-%05d.txt", score,  getpid() );
	FILE *file = fopen( file_name, "w" );
	if( file == NULL ){
		fprintf(stderr, "Error: cannot find file %s", file_name );
		exit( 1 );
	}

	//write result
	fprintf(file, "%d\n", s->length );

	for( i=0; i<s->length; i++ )
		fprintf(file, "%d %d %d %d\n", s->row1[ i ], s->col1[ i ], s->row2[ i ], s->col2[ i ]);


	printf("total cells: %d\n", s->total_cells );
}

//get list of points around a point such that they create a rectangle having size in [min, max]
static struct next_points_struct{
	uint16_t length;
	uint16_t row_delta[1000];
	uint16_t col_delta[1000];
	uint16_t cells_size[1000];
}next_points;

static inline void calculate_next_points(uint16_t min, uint16_t max ){
	size_t i,j;
	next_points.length = 0;
	for( i=1; i<max; i++)
		for(j=1;j<max; j++ )
			if( min <= i*j && i*j <= max ){
				next_points.row_delta[ next_points.length ] = i;
				next_points.col_delta[ next_points.length ] = j;
				next_points.cells_size[ next_points.length ] = i*j;
				 next_points.length ++;
			}

//	printf("%d\n", next_points.length );
//	for( i=0; i<next_points.length; i++ )
//		printf("%d x %d\n", next_points.row_delta[i], next_points.col_delta[i] );
//	exit( 0 );
}

inline size_t count_tomato( uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2 ){
	size_t ret = 0, i, j;
	for( i=x1; i<x2; i++ )
		for( j=y1; j<y2; j++ )
			ret += pizza.data[i][j];
	return ret;
}


inline void reset_slices_t( slices_t *s ){
	size_t i;
	s->total_cells = 0;
	s->length = 0;
	for( i=0; i<1000; i++ ){
		s->row1[ i ] = 0;
		s->col1[ i ] = 0;
		s->row2[ i ] = 0;
		s->col2[ i ] = 0;
	}
}

void cut_pizza( uint16_t row, uint16_t col, slices_t *slices ){
	int i;
	uint16_t row2, col2;
	uint16_t depth       = slices->length;
	uint16_t total_cells = slices->total_cells;
	int cells, tomato;

	if( depth >= 1000 )
		return;

	for( i=next_points.length-1; i>=0; i-- ){
		row2 = row + next_points.row_delta[i];
		col2 = col + next_points.col_delta[i];

		if( row2 <= pizza.columns && col2 <= pizza.rows ){

			cells  = next_points.cells_size[i];

			tomato = count_tomato( row, col, row2, col2 );

			if( tomato >= pizza.min_ingredient && cells - tomato >= pizza.min_ingredient ){
				slices->total_cells = total_cells + cells;
				slices->row1[ depth ] = row;
				slices->col1[ depth ] = col;
				slices->row2[ depth ] = row2;
				slices->col2[ depth ] = col2;
				slices->length = depth + 1;
			}else{

			}

			cut_pizza( row, col2,  slices );
			cut_pizza( row2, col,  slices );

		}else{
			//
			if( slices->total_cells > result.total_cells ){
				//printf("total cells: %d\n", result.total_cells );
				result = *slices;
			}
		}
	}
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
	for (i = 2; i < size; i++){
		printf( "%zu. %s\n", (i-1), strings[i]);
	}

	free (strings);
	fflush( stdout );
}

void signal_handler( int sig ){
	print_result();
	print_execution_trace();
	exit( 1 );
}

int main( int argc, char **argv){
	slices_t slices;

	if( argc != 2 ){
		fprintf(stderr, "Usage: %s file_name\n", argv[0] );
		exit( 1 );
	}

	signal(SIGINT,  signal_handler);
	signal(SIGTERM, signal_handler);

	read_data( argv[1] );
	print_data();

	calculate_next_points( pizza.min_ingredient*2, pizza.max_cells );

	reset_slices_t( &result );
	reset_slices_t( &slices );

	cut_pizza( 0, 0, &slices );

	print_result();

	return 0;
}
