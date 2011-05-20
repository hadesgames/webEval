let () = 
  let ic = open_in "adunare.in" in
  let oc = open_out "adunare.out" in
  try
    Scanf.fscanf ic "%d %d" (fun a b -> Printf.fprintf oc "%d\n" (a + b))
  with e ->
    close_in_noerr ic;
    close_out_noerr oc;
;;
