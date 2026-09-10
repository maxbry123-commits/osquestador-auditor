package org.archive.crawler.framework;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class EngineTest {
    @TempDir
    Path tempDir;

    @Test
    public void testCreateNewJobWithDefaultXmlProfile() throws IOException {
        Path jobsDir = tempDir.resolve("jobsDir");
        Files.createDirectories(jobsDir);
        Path newJobDir = jobsDir.resolve("xmlJob");

        assertTrue(new Engine(jobsDir.toFile()).createNewJobWithDefaults(newJobDir.toFile()));

        assertTrue(Files.exists(newJobDir.resolve("crawler-beans.cxml")));
        assertFalse(Files.exists(newJobDir.resolve("crawler-beans.groovy")));
    }

    @Test
    public void testCreateNewJobWithGroovyProfile() throws IOException {
        Path jobsDir = tempDir.resolve("jobsDir");
        Files.createDirectories(jobsDir);
        Path newJobDir = jobsDir.resolve("groovyJob");

        assertTrue(new Engine(jobsDir.toFile()).createNewJobWithDefaults(newJobDir.toFile(),
                "Defaults (Groovy)"));

        assertTrue(Files.exists(newJobDir.resolve("crawler-beans.groovy")));
        assertFalse(Files.exists(newJobDir.resolve("crawler-beans.cxml")));
    }

    @Test
    public void testCreateNewJobRejectsUnknownProfile() throws IOException {
        Path jobsDir = tempDir.resolve("jobsDir");
        Files.createDirectories(jobsDir);
        Path newJobDir = jobsDir.resolve("badJob");

        assertThrows(IllegalArgumentException.class, () ->
                new Engine(jobsDir.toFile()).createNewJobWithDefaults(newJobDir.toFile(), "bogus"));
        assertFalse(Files.exists(newJobDir));
    }

    @Test
    public void testCreateNewJobFromJobProfile() throws IOException {
        Path jobsDir = tempDir.resolve("jobsDir");
        Path profileDir = jobsDir.resolve("profile-example");
        Files.createDirectories(profileDir);
        String profileConfig = "<!-- profile-example --><beans/>\n";
        Files.write(profileDir.resolve("profile-crawler-beans.cxml"), profileConfig.getBytes());
        Engine engine = new Engine(jobsDir.toFile());

        assertEquals(List.of("Defaults (XML)", "Defaults (Groovy)", "profile-example"),
                engine.getProfileNames());

        Path newJobDir = jobsDir.resolve("copiedJob");

        assertTrue(engine.createNewJobWithDefaults(newJobDir.toFile(),
                "profile-example"));

        assertTrue(Files.exists(newJobDir.resolve("crawler-beans.cxml")));
        assertFalse(Files.exists(newJobDir.resolve("profile-crawler-beans.cxml")));
        assertEquals(profileConfig, Files.readString(newJobDir.resolve("crawler-beans.cxml")));
    }
}
