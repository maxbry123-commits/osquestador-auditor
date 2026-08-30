/*
 * Copyright (c) "Neo4j"
 * Neo4j Sweden AB [https://neo4j.com]
 *
 * This file is part of Neo4j.
 *
 * Neo4j is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
package org.neo4j.kernel.api.impl.index.lucene.v10.codec;

import org.apache.lucene.backward_codecs.lucene103.Lucene103Codec;
import org.apache.lucene.codecs.Codec;
import org.apache.lucene.codecs.FilterCodec;
import org.apache.lucene.codecs.KnnVectorsFormat;

/// Compatibility codec that is being loaded from existing vector-3.0 indexes
public class VectorCodecV3 extends FilterCodec implements Lucene10Codec {
    private static final String CODEC_NAME = "VectorCodecV3";
    private final KnnVectorsFormat vectorFormat;

    /// Used by Lucene Service Loader for reading from segments
    /// Do not use this codec for writing
    public VectorCodecV3() {
        super(CODEC_NAME, new Lucene103Codec());
        this.vectorFormat = new CompatibilityKnnVectorFormatV3();
    }

    @Override
    public KnnVectorsFormat knnVectorsFormat() {
        return vectorFormat;
    }

    @Override
    public Codec codec() {
        return this;
    }
}
