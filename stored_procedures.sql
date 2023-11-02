
DROP PROCEDURE IF EXISTS getNewBookId;
CREATE PROCEDURE getNewBookId (INT id OUTPUT)
    BEGIN
        SELECT max(bookId) from Books);
    END //

CREATE PROCEDURE getNewAuthorId ()
    BEGIN
        SELECT max(authorId) from Authors;
    END //

CREATE PROCEDURE getAuthorIdFromName (VARCHAR fname, VARCHAR lname)
    BEGIN
        SELECT authorId FROM Authors a WHERE a.firstname = @fname AND a.lastname = @lname;
    END //

