function ODF = get_ODF_from_CRC_file(CRC_file_path, specimenSym, phase)
    ebsd = loadEBSD_crc(CRC_file_path);
    ori = ebsd(phase).orientations;
    ori.SS = specimenSymmetry(specimenSym);
    ODF = calcDensity(ori);
end
