PROGRAM Main;

PROCEDURE Alpha(a : INTEGER; b : INTEGER);
VAR x : INTEGER;
BEGIN
   x := (a + b ) * 2;
END;

BEGIN { Main }

   Alpha(3 + 5, 7);  { procedure call }

END.  { Main }