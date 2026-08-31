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
package org.neo4j.kernel.api.impl.index.lucene;

import java.io.Closeable;
import java.io.IOException;

public interface LuceneDirectoryReader extends Closeable {
    String KEY_STATUS = "status";
    String ONLINE = "online";

    boolean isOnline() throws IOException;

    /**
     * Creates a new {@link LuceneSearcherManager} that will manage multiple searchers.
     * The manager needs to be closed after usage, and this will also close all underlying
     * managed {@link LuceneIndexSearcher}.
     *
     * @return a new searcher manager.
     */
    LuceneSearcherManager newSearcherManager() throws IOException;

    /**
     * Create a new direct {@link LuceneIndexSearcher}. Direct means that it's not owned
     * by a {@link LuceneSearcherManager} and care must be taken to properly close the
     * searcher when done using it.
     *
     * @return a new searcher.
     */
    LuceneIndexSearcher newDirectSearcher();
}
