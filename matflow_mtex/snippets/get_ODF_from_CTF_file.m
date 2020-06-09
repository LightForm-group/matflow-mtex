function ODF = get_ODF_from_CTF_file(CTF_file_path, specimenSym, phase)
    ebsd = loadEBSD_ctf(CTF_file_path);
    ori = ebsd(phase).orientations;
    ori.SS = specimenSymmetry(specimenSym);
    ODF = calcDensity(ori);
end
