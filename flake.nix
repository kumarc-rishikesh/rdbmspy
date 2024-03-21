{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs {
            inherit system ;
          };
        in
        with pkgs;
        {
          devShells.default = mkShell {
            buildInputs = [ 
            python311Full
            python311Packages.pyparsing 
            python311Packages.ipykernel
            python311Packages.nuitka
             ];
            shellHook = ''
            source="sql-parser/main.py"
            binary="main.bin"
            if ! [ -e "$binary" ]; then
              echo "Binary does not exist. Building...."
              nuitka3 --follow-imports sql-parser/main.py
            else
              echo "Binary already exists. Build skipped"
            fi
            '';
          };
        }
      );
}
