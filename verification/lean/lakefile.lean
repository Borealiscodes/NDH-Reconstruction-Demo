import Lake
open Lake Target

package «ndh_invariants» where
  -- Add package configuration options here

lean_lib «NdhInvariants» where
  -- Add library configuration options here

@[default_target]
lean_exe «ndh_verify» where
  root := `Main
  supportInterpreter := true
