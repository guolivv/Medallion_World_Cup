CREATE TABLE IF NOT EXISTS player (
    number               SMALLINT,
    pos                  VARCHAR(10),
    name                 VARCHAR(100) NOT NULL,
    date_of_birth        DATE,
    club_name            VARCHAR(100),
    club_country         VARCHAR(50),
    confederation_name   VARCHAR(50) NOT NULL,
    fifa_code            VARCHAR(3) NOT NULL REFERENCES team(fifa_code),
    CONSTRAINT uq_player_name_confederation UNIQUE (confederation_name, name)
);

CREATE INDEX idx_player_fifa_code ON player (fifa_code);
CREATE INDEX idx_player_confederation ON player (confederation_name, name);