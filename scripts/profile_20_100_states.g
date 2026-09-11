# Memory measurement ONLY. This deliberately does no proof checking.
# Read a closed n=7 prefix after this file; exit after one million states.
ProbeStates:=[];;
ProbeStarted:=Runtime();;
StartProof:=function(n,bound)
    Assert(0,n=7 and bound=8);
    Print("MEMORY_PROBE_ONLY n=7 no_proof_checking\n");
end;
CheckNode:=function(identifier,state,perm,children)
    Assert(0,identifier=Length(ProbeStates)+1);
    Add(ProbeStates,state);
    if identifier in [100000,500000,1000000] then
        GASMAN("collect");
        Print("MEMORY_PROBE nodes=",identifier," reachable_bytes=",MemoryUsage(ProbeStates),
              " cpu_ms=",Runtime()-ProbeStarted,"\n");
    fi;
    if identifier=1000000 then
        Print("MEMORY_PROBE_DONE no_verification_claim\n");
        QUIT_GAP(0);
    fi;
end;
