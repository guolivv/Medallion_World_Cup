CREATE TABLE IF NOT EXISTS goal (
    name                   VARCHAR(100) NOT NULL,
    minute                 SMALLINT NOT NULL,
    owngoal                BOOLEAN NOT NULL DEFAULT FALSE,
    penalty                BOOLEAN NOT NULL DEFAULT FALSE,
    team_name              VARCHAR(50) NOT NULL, 
    rival_team_name        VARCHAR(50) NOT NULL,
    ground                 VARCHAR(100),
    CONSTRAINT chk_goals_teams_different CHECK (team_name <> rival_team_name),
    CONSTRAINT fk_goal_team_team_name FOREIGN KEY (team_name) REFERENCES team(name),
    CONSTRAINT fk_goal_team_rival_team_name FOREIGN KEY (rival_team_name) REFERENCES team(name)
);

CREATE INDEX idx_goal_name_team_name ON goal (name, team_name);
CREATE INDEX idx_goal_rival_team_name ON goal (rival_team_name);


CREATE OR REPLACE FUNCTION check_player_goal_condition()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.owngoal = FALSE THEN
        IF NOT EXISTS (
            SELECT 1 FROM player 
            WHERE name = NEW.name AND confederation_name = NEW.team_name
        ) THEN
            RAISE EXCEPTION 'Erro: O jogador % não joga no time %.', NEW.name, NEW.team_name;
        END IF;
    ELSE
        IF NOT EXISTS (
            SELECT 1 FROM player 
            WHERE name = NEW.name AND confederation_name = NEW.rival_team_name
        ) THEN
            RAISE EXCEPTION 'Erro (Gol Contra): O jogador % não joga no time rival %.', NEW.name, NEW.rival_team_name;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_goal_player
BEFORE INSERT OR UPDATE ON goal
FOR EACH ROW EXECUTE FUNCTION check_player_goal_condition();