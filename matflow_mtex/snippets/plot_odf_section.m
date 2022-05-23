function exitcode = plot_odf_section(orientationsPath, use_contours, IPF_reference_direction, optionsPath)

    allOriData = jsondecode(fileread(orientationsPath));
    allOpts = jsondecode(fileread(optionsPath));

    for PFIdx = 1:length(allOriData)

        ori_data = allOriData(PFIdx);
        crystalSym = ori_data.crystal_symmetry;

        alignment = {};

        if isfield(ori_data.unit_cell_alignment, 'x')
            alignment{end + 1} = sprintf('X||%s', ori_data.unit_cell_alignment.x);
        end

        if isfield(ori_data.unit_cell_alignment, 'y')
            alignment{end + 1} = sprintf('Y||%s', ori_data.unit_cell_alignment.y);
        end

        if isfield(ori_data.unit_cell_alignment, 'z')
            alignment{end + 1} = sprintf('Z||%s', ori_data.unit_cell_alignment.z);
        end

        crystalSym = crystalSymmetry(crystalSym, alignment{:});

        if strcmp(ori_data.type, 'quat')

            quat_data = ori_data.quaternions;

            if ori_data.P == 1
                % Scale vector part by -1:
                % This works "accidentally" - the requirement for inverting is due to
                % MTEX adopting a crystal->specimen convention rather than specimen->crystal
                % needs fixing!
                quat_data(:, 2:end) = quat_data(:, 2:end) * -1;
            end

            if strcmp(ori_data.quat_component_ordering, 'vector-scalar')
                % Swap to scalar-vector order:
                quat_data = circshift(quat_data, 1, 2);
            end

            quats = quaternion(quat_data.');
            orientations = orientation(quats, crystalSym);

        elseif strcmp(ori_data.type, 'euler')

            if ori_data.euler_degrees
                orientations = orientation.byEuler( ...
                    ori_data.euler_angles * degree, ...
                    crystalSym ...
                );
            else
                orientations = orientation.byEuler( ...
                    ori_data.euler_angles, ...
                    crystalSym ...
                );
            end

        end

        newMtexFigure('layout', [1, 1], 'visible', 'off');
        plotx2east;
        odf = calcDensity(orientations, 'kernel', deLaValleePoussinKernel, 'halfwidth', 5 * degree);
        plotSection(odf, 'contourf', 'phi2', 45 * degree, 'minmax');
        mtexColorbar ('location', 'southoutside', 'title', 'mrd', 'FontSize', 24);

        if isfield(allOpts, "colourbar_limits")
            CLim(gcm, allOpts.colourbar_limits);
        end

        if isfield(allOpts, "use_one_colourbar")
            mtexColorbar % remove colorbars
            CLim(gcm, 'equal');
            mtexColorbar % add a single colorbar
        end

        if isfield(ori_data, 'increment')
            fileName = sprintf('odf_section_inc_%d.png', ori_data.increment);
        else
            fileName = 'odf_section.png';
        end

        saveFigure(fileName);

        if PFIdx == 1 && ~use_contours
            newMtexFigure('layout', [1, 1], 'visible', 'off');
            plot(ipfKey);
            saveFigure('IPF_key.png');
        end

        close all;

    end

    exitcode = 1;
end
