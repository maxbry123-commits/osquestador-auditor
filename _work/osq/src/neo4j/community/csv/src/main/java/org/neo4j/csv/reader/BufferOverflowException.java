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
package org.neo4j.csv.reader;

public class BufferOverflowException extends IllegalStateException {
    public BufferOverflowException(int chunkSize, String sourceDescription, long lineNumber) {
        super("Tried to read a field larger than buffer size " + chunkSize
                + ". A common cause of this is that a field has an unterminated "
                + "quote and so will try to seek until the next quote, which ever line it may be on."
                + " This should not happen if multi-line fields are disabled, given that the fields contains "
                + "no new-line characters. This field started at "
                + sourceDescription + ":" + lineNumber);
    }
}
