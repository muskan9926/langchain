CREATE SCHEMA langchaindbo;

CREATE TABLE `user_sessions` (
  `id` bigint(10) NOT NULL AUTO_INCREMENT,
  `session_id` varchar(255) NOT NULL,
  `created_on` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_on` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);



CREATE TABLE loan_documents (
  id bigint(10) NOT NULL AUTO_INCREMENT,
  document_name varchar(255) NOT NULL,
  collection_name varchar(255) NOT NULL,  
  created_on datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_on datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY document_name_UNIQUE (document_name)
);








-- DELIMITER //

-- CREATE PROCEDURE InsertOrUpdateUserSession(
--     IN personIdParam BIGINT,
--     IN sessionIdParam VARCHAR(255),
--     OUT newSessionIdParam VARCHAR(255)
-- )
-- BEGIN
--     DECLARE existingSessionId VARCHAR(255);
--     DECLARE uniqueSessionId VARCHAR(255);

--     -- Check if the session ID already exists
--     SELECT session_id INTO existingSessionId
--     FROM user_sessions
--     WHERE session_id = sessionIdParam;

--     IF existingSessionId IS NOT NULL THEN
--         -- Generate a new unique session ID
--         SET uniqueSessionId = CONCAT(sessionIdParam, '_', UUID());
--     ELSE
--         SET uniqueSessionId = sessionIdParam;
--     END IF;

--     -- Insert the session record
--     INSERT INTO user_sessions (person_id, session_id)
--     VALUES (personIdParam, uniqueSessionId);

--     -- Return the generated session ID
--     SET newSessionIdParam = uniqueSessionId;
-- END //

-- DELIMITER ;
