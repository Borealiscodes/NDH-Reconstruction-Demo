import Lake
open Lake RCurl

package «ndh_verification» where
  -- Add package configuration options here

@[default_target]
lean_lib «NdhVerification» where
  srcDir := "src"

require mathlib from git
  "https://github.com"
