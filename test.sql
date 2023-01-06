
DROP TABLE users;

CREATE TABLE users (
    user_id INT UNSIGNED , 
    username VARCHAR(20) , 
    user_password VARCHAR(20) ,
    PRIMARY KEY (user_id)
);

INSERT INTO users VALUES (1209 , 'Lody' , 'impostor');

