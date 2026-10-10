BEGIN TRANSACTION;
CREATE TABLE email_relay (
        id          INTEGER PRIMARY KEY,
        name        varchar (80),
        value       varchar (100)
);
COMMIT;
