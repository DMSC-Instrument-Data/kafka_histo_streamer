#  -*- coding: utf-8 -*-

import time
import flatbuffers
from fbschema import \
    EventHistogram, Array, ArrayDouble, DimensionMetaData


class Workspace2DSerializer(object):
    def __init__(self, workspace):
        self._ws = workspace

    def serialize(self):
        self._dimcount = self._ws.getNumDims()
        self._bincount = self._ws.getNumberBins()
        self._shape = [self._bincount + 1, self._ws.getNumberHistograms()]

        # TODO: Better size approx?
        builder = flatbuffers.Builder(16)

        source = builder.CreateString('Mantid')
        timestamp = long(time.time() * 1e9)
        dim_metadata = self._do_metadata(builder)
        last_metadata_timestamp = timestamp
        current_shape = self._do_shape(builder)
        # offset = 0
        data = self._do_data(builder)
        # errors = self._do_errors(builder)
        # info = 0

        # Build the Flatbuffer
        EventHistogram.EventHistogramStart(builder)
        EventHistogram.EventHistogramAddSource(builder, source)
        EventHistogram.EventHistogramAddTimestamp(builder, timestamp)
        if dim_metadata:
            EventHistogram.EventHistogramAddDimMetadata(builder, dim_metadata)
        EventHistogram.EventHistogramAddLastMetadataTimestamp(builder, last_metadata_timestamp)
        EventHistogram.EventHistogramAddCurrentShape(builder, current_shape)
        # EventHistogram.EventHistogramAddOffset(builder, offset)
        EventHistogram.EventHistogramAddDataType(builder, Array.Array.ArrayDouble)
        EventHistogram.EventHistogramAddData(builder, data)
        # EventHistogram.EventHistogramAddErrorsType(builder, Array.Array.ArrayDouble)
        # EventHistogram.EventHistogramAddErrors(builder, errors)
        # EventHistogram.EventHistogramAddInfo(builder, info)
        root = EventHistogram.EventHistogramEnd(builder)
        builder.Finish(root)

        # Generate the output and replace the file_identifier
        buff = builder.Output()
        buff[4:8] = bytes('hs00')
        return bytes(buff)

    def _do_metadata(self, builder):
        dims = []
        for index in reversed(range(self._dimcount)):
            dim = self._ws.getDimension(index)
            axis = self._ws.getAxis(index)

            length = dim.getNBins()
            label = builder.CreateString(dim.getName())
            bin_boundaries = 0

            # Counts are treated differently from other dimensions
            if dim.getUnits():
                # e.g.: 'TOF'
                unit = builder.CreateString(axis.getUnit().unitID())
            else:
                # e.g.: 'Counts'
                unit = builder.CreateString(self._ws.YUnit())

            # To determine if this dimension contains bins
            nbounds = dim.getNBoundaries()
            if nbounds == length + 1:
                ArrayDouble.ArrayDoubleStartValueVector(builder, nbounds)
                for bindex in reversed(range(nbounds)):
                    builder.PrependFloat64(dim.getX(bindex))
                bounds = builder.EndVector(nbounds)
                ArrayDouble.ArrayDoubleStart(builder)
                ArrayDouble.ArrayDoubleAddValue(builder, bounds)
                bin_boundaries = ArrayDouble.ArrayDoubleEnd(builder)

            # Build dimension
            DimensionMetaData.DimensionMetaDataStart(builder)
            DimensionMetaData.DimensionMetaDataAddLength(builder, length)
            if unit:
                DimensionMetaData.DimensionMetaDataAddUnit(builder, unit)
            DimensionMetaData.DimensionMetaDataAddLabel(builder, label)
            if bin_boundaries:
                DimensionMetaData.DimensionMetaDataAddBinBoundariesType(
                    builder, Array.Array.ArrayDouble)
                DimensionMetaData.DimensionMetaDataAddBinBoundaries(
                    builder, bin_boundaries)

            dims.append(DimensionMetaData.DimensionMetaDataEnd(builder))

        EventHistogram.EventHistogramStartDimMetadataVector(
            builder, self._dimcount)
        for dim in dims:
            builder.PrependUOffsetTRelative(dim)
        return builder.EndVector(self._dimcount)

    def _do_shape(self, builder):
        EventHistogram.EventHistogramStartCurrentShapeVector(
            builder, self._dimcount)
        for size in reversed(self._shape):
            builder.PrependUint32(size)
        return builder.EndVector(self._dimcount)

    def _do_data(self, builder):
        # datalen = self._ws.getNumberBins() * self._ws.getNumberHistograms()
        bytedata = self._ws.extractY().tobytes()
        bytelen = len(bytedata)
        datalen = bytelen / 8  # flatbuffers.number_types.Uint32Flags.bytewidth
        ArrayDouble.ArrayDoubleStartValueVector(builder, datalen)

        # Manually move header to make room for data
        head = flatbuffers.number_types.UOffsetTFlags.py_type(
            builder.Head() - bytelen)
        builder.head = head
        builder.Bytes[head:head+bytelen] = bytedata[0:bytelen]

        data = builder.EndVector(datalen)
        ArrayDouble.ArrayDoubleStart(builder)
        ArrayDouble.ArrayDoubleAddValue(builder, data)
        return ArrayDouble.ArrayDoubleEnd(builder)

    def _do_errors(self, builder):
        return 0
