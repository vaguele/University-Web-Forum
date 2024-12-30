CREATE TABLE loginInfo (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Username varchar(255),
    Password varchar(255)
);

Create Table dashboardPosts(
    Id INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    Post_Body Text,
    time_posted Date,
    rating INT,
    FOREIGN KEY (userId) REFERENCES loginInfo(Id)
)

Create Table placeSportClassRating(
    Id Int AUTO_INCREMENT UNIQUE KEY,
    name varchar(255) PRIMARY KEY,
    likes Int

)

Create Table Posts(
    Id INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    Post_Body Text,
    time_posted Date,
    rating INT,
    replyTo Int,
    tag varchar(255),
    FOREIGN KEY (userId) REFERENCES loginInfo(Id)
)

Create Table whoAlreadyLikedPSC(
    UserId INT,
    PSCName varchar(255),
    likeOrDislike varchar(255),
    FOREIGN KEY (UserId) REFERENCES loginInfo(Id),
    FOREIGN KEY (PSCName) REFERENCES placeSportClassRating(name)
)

Create Table whoAlreadyLikedPost(
    UserId INT,
    PostID INT,
    likeOrDislike varchar(255),
    FOREIGN KEY (UserId) REFERENCES loginInfo(Id),
    FOREIGN KEY (PostID) REFERENCES Posts(Id)
)


