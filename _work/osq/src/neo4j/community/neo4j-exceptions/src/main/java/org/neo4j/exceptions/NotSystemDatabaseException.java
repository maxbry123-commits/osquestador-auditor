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
package org.neo4j.exceptions;

import static org.neo4j.kernel.database.NamedDatabaseId.SYSTEM_DATABASE_NAME;

import org.neo4j.gqlstatus.ErrorGqlStatusObject;
import org.neo4j.gqlstatus.ErrorGqlStatusObjectImplementation;
import org.neo4j.gqlstatus.GqlParams;
import org.neo4j.gqlstatus.GqlStatusInfoCodes;
import org.neo4j.kernel.api.exceptions.Status;

/**
 * Thrown when the operation <STRONG>requires</STRONG> the system database but was executed on another.
 * <p>
 * Not to be confused with the opposite {@link org.neo4j.exceptions.DisallowedOnSystemException}
 * which is thrown when the operation is <STRONG>not allowed on</STRONG> the system database.
 * <p>
 * GQL status code: 51N28
 */
public class NotSystemDatabaseException extends InvalidTargetDatabaseException {

    private NotSystemDatabaseException(ErrorGqlStatusObject gqlStatusObject, String message) {
        super(gqlStatusObject, message);
    }

    @Override
    public Status status() {
        return Status.Statement.NotSystemDatabaseError;
    }

    public static NotSystemDatabaseException notSystemDatabaseException(String commandName) {
        var gql = ErrorGqlStatusObjectImplementation.from(GqlStatusInfoCodes.STATUS_51N28)
                .withParam(GqlParams.StringParam.db, SYSTEM_DATABASE_NAME)
                .build();
        return new NotSystemDatabaseException(
                gql,
                "This is an administration command and it should be executed against the system database: %s"
                        .formatted(commandName));
    }
}
