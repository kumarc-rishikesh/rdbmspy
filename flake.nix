{
  inputs = { 
    nixpkgs.url = "github:NixOS/nixpkgs?ref=release-23.11";
  };

  outputs = { self, nixpkgs }:
    let pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in {
      devShell.x86_64-linux =
        pkgs.mkShell { 
          buildInputs = with pkgs; [ 
          python311Full
          python311Packages.pyparsing 
          python311Packages.ipykernel
          ]; 
      };
   };
}
