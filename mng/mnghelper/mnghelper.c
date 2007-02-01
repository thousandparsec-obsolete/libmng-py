/*
 * This file is a speed up wrapper for libmng-py.
 *
 * It moves all the calculations which are preformed often into pure C.
 */

typedef struct {
	void* object; 			/* Pointer to Python object */
	void* buffer; 			/* Pointer to a memory buffer */
	int   buffer_size; 		/* How long the buffer is */
	int   height;           /* Height of the image */
	int   width; 			/* Width of the image */
	int   bytesperpixel; 	/* Number of bytes each pixel uses */
	int   bytesperalpha; 	/* Number of bytes each pixel of alpha uses */
} cmng_data;

#include <string.h>
#include <libmng.h>

mng_ptr* getcanvasline(mng_handle handle, mng_uint32 line) {
	cmng_data* data = (cmng_data*)mng_get_userdata(handle);

	if (data->buffer == NULL) {
		printf("getcanvasline (C) was called when there was no buffer!\n");
		return NULL;
	}

	void* p = data->buffer + (data->width*line*data->bytesperpixel);
	if (p-(data->buffer) > data->buffer_size) {
		printf("getcanvasline (C) had an error, we ran off the bottom of a buffer! (%d  > %d)\n", p-(data->buffer), data->buffer_size);
		return NULL;
	}

	/* Clear the memory first - FIXME: Figure out why this is needed and explain it */
//	memset(p, 0, data->width*data->bytesperpixel);
	return p;
}

/*
 * getalphaline is called when the alpha channel is separated from the
 * other pixels.
 */
mng_ptr* getalphaline(mng_handle handle, mng_uint32 line) {
	cmng_data* data = (cmng_data*)mng_get_userdata(handle);

	if (data->buffer == NULL) {
		printf("getalphaline (C) was called when there was no buffer!\n");
		return NULL;
	}
	if (data->bytesperalpha == 0) {
		printf("getalphaline (C) was called when the bytesperalpha was zero!\n");
		return NULL;
	}

	void* p = data->buffer + (data->width*data->height*data->bytesperpixel)
									  + (data->width*line*data->bytesperalpha);
	// Clear the memory first - FIXME: Figure out why this is needed and explain it
//	memset(p, 0, data->width*data->bytesperalpha);
	return p;
}

mng_ptr* mngalloc(mng_uint32 i) {
	return (mng_ptr*)calloc(1, i);
}

void mngfree(mng_ptr* p, mng_uint32 i) {
	free(p);
}

mng_bool mngrefresh_dummy(mng_handle* handle, mng_uint32 x, mng_uint32 y, mng_uint32 w, mng_uint32 h) {
	return 1;
}
