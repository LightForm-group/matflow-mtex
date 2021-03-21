function ODF = get_ODF_from_CRC_file(CRC_file_path, referenceFrameTransformation, specimenSym, phase, rotationJSONPath)
    
    if isempty(referenceFrameTransformation)
        referenceFrameTransformation = {};
    else
        referenceFrameTransformation = {referenceFrameTransformation};
    end

    ebsd = loadEBSD_crc(CRC_file_path, referenceFrameTransformation{:});
    
    rotationJSON = jsondecode(fileread(rotationJSONPath));
    if ~isempty(rotationJSON)
        % Note that using rotate appears to remove the non-indexed phase.
        rotationEulersRad = num2cell(rotationJSON.euler_angles_deg * degree);
        rot = rotation('euler', rotationEulersRad{:});
        if isfield(rotationJSON, 'keep_XY')
            ebsd = rotate(ebsd, rot, 'keepXY');
        elseif isfield(rotationJSON, 'keep_euler')
            ebsd = rotate(ebsd, rot, 'keepEuler');
        else
            ebsd = rotate(ebsd, rot);
        end
    end

    ori = ebsd(phase).orientations;
    ori.SS = specimenSymmetry(specimenSym);
    ODF = calcDensity(ori);
end
