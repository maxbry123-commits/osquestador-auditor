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
package org.neo4j.server.security.auth;

/**
 * An interface for performing validity checks, such as checking if a user account is suspended or expired, or checking the expiry of tokens.
 * These are intended to be checked at authorization to make sure that the authentication is still valid.
 * The checks are are not necessary at authentication time because the authentication itself will fail anyway for the same reasons that these checks would
 * The whole point of these checks is to catch changes that may have happened after authentication, but before authorization.
 */
public interface ValidityCheck {
    void validate();
}
