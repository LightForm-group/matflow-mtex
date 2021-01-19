function exitcode = export_orientations_JSON(orientations, fileName)
    
    oris_dat = {};
    oris_dat.type = 'euler';
    oris_dat.unit_cell_alignment = prepare_crystal_alignment(orientations.CS);
    oris_dat.euler_angles = [...
        orientations.phi1,...
        orientations.Phi,...
        orientations.phi2...
    ] / degree;
    oris_dat.euler_degrees = 'True';

    jsonStr = jsonencode(oris_dat);
    
    fid = fopen(fileName, 'w');    
    fwrite(fid, jsonStr, 'char');
    fclose(fid);        

    exitcode = 1;
    
end

function alignment = prepare_crystal_alignment(crystalSym)
    if isempty(crystalSym.alignment)
        % Cubic
        alignment = {};
        alignment.x = 'a';
        alignment.y = 'b';
        alignment.z = 'c';
    else
        align1 = split(crystalSym.alignment{1}, '||');
        align2 = split(crystalSym.alignment{2}, '||');
        align3 = split(crystalSym.alignment{3}, '||');
        alignment = {};
        alignment = setfield(alignment, lower(align1{1}), align1{2});
        alignment = setfield(alignment, lower(align2{1}), align2{2});
        alignment = setfield(alignment, lower(align3{1}), align3{2});
    end
end
