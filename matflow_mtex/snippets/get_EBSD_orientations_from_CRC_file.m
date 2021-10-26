function EBSD_orientations = get_EBSD_orientations_from_CRC_file(CRC_file_path, referenceFrameTransformation, specimenSym, phase, rotationJSONPath)

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

    EBSD_orientations = ebsd(phase).orientations;
    EBSD_orientations.SS = specimenSymmetry(specimenSym);
end
