# Explicit permutation generators for the group in Problem 4.55.
# Obtained from PerfectGroup(7560,1); subsequent checks construct the group
# from these permutations directly.
Group455:=function()
return Group(
 (1,2,3)(4,10,8,15,6,11)(5,13,9,17,7,14)(12,16,18)
 (19,31,27,36,21,32)(20,34,28,38,22,35)(23,33,29,41,25,37)
 (24,39,30,42,26,40)(43,44,45),
 (1,4,12,5)(2,6,16,7)(3,8,18,9)(10,19,33,20)(11,21,37,22)
 (13,23,39,24)(14,25,40,26)(15,27,41,28)(17,29,42,30)
 (34,43)(35,44)(38,45));
end;
