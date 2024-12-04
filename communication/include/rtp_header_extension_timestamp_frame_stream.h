#pragma once

#include <gst/gst.h>
#include <gst/rtp/gstrtphdrext.h>

typedef struct _GstRTPHeaderExtensionTimestampFrameStream {
	GstRTPHeaderExtension parent;

} GstRTPHeaderExtensionTimestampFrameStream;

typedef struct _GstRTPHeaderExtensionTimestampFrameStreamClass {
	GstRTPHeaderExtensionClass parent_class;
} GstRTPHeaderExtensionTimestampFrameStreamClass;

#define TIMESTAMP_FRAME_STREAM_HDR_EXT_URI "timestamp-frame-stream:1.0"

#define GST_TYPE_RTP_HEADER_EXTENSION_TIMESTAMP_FRAME_STREAM (gst_rtp_header_extension_timestamp_frame_stream_get_type())
#define GST_RTP_HEADER_EXTENSION_TIMESTAMP_FRAME_STREAM(obj) (G_TYPE_CHECK_INSTANCE_CAST((obj), GST_TYPE_RTP_HEADER_EXTENSION_TIMESTAMP_FRAME_STREAM, GstRTPHeaderExtensionTimestampFrameStream))
#define GST_RTP_HEADER_EXTENSION_TIMESTAMP_FRAME_STREAM_CLASS(klass) (G_TYPE_CHECK_CLASS_CAST((klass), GST_TYPE_RTP_HEADER_EXTENSION_TIMESTAMP_FRAME_STREAM, GstRTPHeaderExtensionTimestampFrameStreamClass))
#define GST_IS_RTP_HEADER_EXTENSION_TIMESTAMP_FRAME_STREAM(obj) (G_TYPE_CHECK_INSTANCE_TYPE((obj), GST_TYPE_RTP_HEADER_EXTENSION_TIMESTAMP_FRAME_STREAM))
#define GST_IS_RTP_HEADER_EXTENSION_TIMESTAMP_FRAME_STREAM_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), GST_TYPE_RTP_HEADER_EXTENSION_TIMESTAMP_FRAME_STREAM))

GType gst_rtp_header_extension_timestamp_frame_stream_get_type(void);
GST_ELEMENT_REGISTER_DECLARE(rtp_header_extension_timestamp_frame_stream)