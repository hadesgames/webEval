with Ada.Integer_Text_IO, Ada.Text_IO;
use Ada.Integer_Text_IO, Ada.Text_IO;

procedure adun is
   A, B : Integer;
   InFile, OutFile : FILE_TYPE;
begin
   Create (OutFile, Out_File, "adun.out");
   Open (InFile, In_File, "adun.in");

   Get(InFile, A);
   Get(InFile, B);
--   Ada.Integer_Text_Io.Get (Item => A);
--   Ada.Integer_Text_Io.Get (Item => B);
   Put(OutFile, A+B);
   Close(InFile);
   Close(OutFile);
end adun;
 
