CREATE DATABASE faculties_recommender;

CREATE TABLE faculties (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE keywords (
    id INT PRIMARY KEY AUTO_INCREMENT,
    word VARCHAR(50) NOT NULL,
    idf DOUBLE NOT NULL
);
CREATE TABLE faculties_keywords (
    faculty_id INT NOT NULL,
    keyword_id INT NOT NULL,
    tf DOUBLE NOT NULL,
    PRIMARY KEY (faculty_id, keyword_id),
    FOREIGN KEY (faculty_id) REFERENCES faculties(id),
    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

CREATE INDEX idx_keywords_name ON keywords (word);
CREATE INDEX idx_faculties_keyword_id ON faculties_keywords(keyword_id);