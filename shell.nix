{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    #~ pkgs.gnumake
    (pkgs.python3.withPackages (ps: with ps; [
      ics
    ]))
  ];
}
