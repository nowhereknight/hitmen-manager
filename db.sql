
use postgres;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp"

drop table hits;

drop table hitmen;

CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
      
CREATE OR REPLACE FUNCTION trigger_set_expiration_time()
RETURNS TRIGGER AS $$
BEGIN
   NEW.expiration_time = NOW() + NEW.expiration_time_in_minutes * INTERVAL '1 minute';
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;


create table Hitmen(
hitman_uuid uuid DEFAULT uuid_generate_v4(),
name varchar(100) NOT NULL,
lastname_1 varchar(100) NOT NULL,
lastname_2 varchar(100),
email varchar(50) NOT NULL UNIQUE,
password varchar(200),
status varchar(20),
rank varchar(20),
manager_uuid uuid,
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
primary key(hitman_uuid),
CONSTRAINT fk_managers FOREIGN KEY(manager_uuid) 
REFERENCES Hitmen(hitman_uuid)
);


CREATE TRIGGER set_timestamp
 BEFORE UPDATE ON Hitmen
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_timestamp();
   
   
create table Hits(
hit_uuid uuid DEFAULT uuid_generate_v4(),
identifier varchar(20) NOT NULL,
description varchar(100) NOT NULL,
target_name varchar(100) NOT NULL,
target_lastname_1 varchar(100) NOT NULL,
target_lastname_2 varchar(100),username varchar(100) NOT NULL UNIQUE,
status varchar(20),
hitman_uuid uuid,
creator_uuid uuid,
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
primary key(hit_uuid),
CONSTRAINT fk_asignees FOREIGN KEY(hitman_uuid) 
REFERENCES Hitmen(hitman_uuid),
CONSTRAINT fk_creators FOREIGN KEY(creator_uuid) 
REFERENCES Hitmen(hitman_uuid)
);

CREATE TRIGGER set_timestamp
 BEFORE UPDATE ON Hits
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_timestamp();

   
INSERT INTO public.hitmen
(hitman_uuid, "name", lastname_1, email, "password", status, "rank", created_at, updated_at)
VALUES(uuid_generate_v4(), 'Giuseppi', 'Palafox', 'giuseppi@gmail.com', '12QwAsZx./', 'active', 'god', now(), now());
