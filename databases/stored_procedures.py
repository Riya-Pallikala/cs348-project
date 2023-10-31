DELIMITER //
DROP PROCEDURE IF EXISTS getNewBookId;
CREATE PROCEDURE getNewBookId (INT id OUTPUT)
    BEGIN
        DECLARE maxval int default 0;
        SET maxval = (SELECT max(bookId) from Books);

        if (maxval is None):
            SET @id = 1
        else:
            SET @id = maxval + 1
    END //

CREATE PROCEDURE getNewAuthorId (INT id OUTPUT)
    BEGIN
        DECLARE maxval int default 0;
        SET maxval = (SELECT max(authorId) from Authors);

        if (maxval is None):
            SET @id = 1
        else:
            SET @id = maxval + 1
    END //

CREATE PROCEDURE getAuthorIdFromName (VARCHAR fname, VARCHAR lname, INT id OUTPUT)
    BEGIN
        DECLARE aId int default 0;
        SET aId = (SELECT authorId FROM Authors a WHERE a.firstname = @fname AND a.lastname = @lname);

        if (aId is None):
            SET @id = None
        else:
            SET @id = aId + 1
    END //
DELIMITER;
