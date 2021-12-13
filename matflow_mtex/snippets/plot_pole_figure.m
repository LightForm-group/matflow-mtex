function exitcode = plot_pole_figure(orientationsPath, poleFigureDirections, use_contours, IPF_reference_direction)

    allOriData = jsondecode(fileread(orientationsPath));

    for PFIdx = 1:length(allOriData)

        ori_data = allOriData(PFIdx);
        crystalSym = ori_data.crystal_symmetry

        alignment = {};

        if isfield(ori_data.unit_cell_alignment, 'x');
            alignment{end + 1} = sprintf('X||%s', ori_data.unit_cell_alignment.x);
        end

        if isfield(ori_data.unit_cell_alignment, 'y');
            alignment{end + 1} = sprintf('Y||%s', ori_data.unit_cell_alignment.y);
        end

        if isfield(ori_data.unit_cell_alignment, 'z');
            alignment{end + 1} = sprintf('Z||%s', ori_data.unit_cell_alignment.z);
        end

        crystalSym = crystalSymmetry(crystalSym, alignment{:});
        millerDirs = Miller(poleFigureDirections{1}, crystalSym);

        for i = 2:length(poleFigureDirections)
            newMillerDir = Miller(poleFigureDirections{i}, crystalSym);
            millerDirs = [millerDirs, newMillerDir];
        end

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

        if use_contours
            plotPDF(orientations, millerDirs, 'contourf');
            mtexColorbar;
        else
            ipfKey = ipfColorKey(crystalSym);
            ipfKey.inversePoleFigureDirection = vector3d.(upper(IPF_reference_direction));
            oriColors = ipfKey.orientation2color(orientations);
            plotPDF( ...
                orientations, ...
                millerDirs, ...
                'property', oriColors ...
            );

        end

        aAxis = Miller(crystalSym.aAxis, 'xyz');
        bAxis = Miller(crystalSym.bAxis, 'xyz');
        cAxis = Miller(crystalSym.cAxis, 'xyz');

        xyzVecs = eye(3);
        xyzLabels = {'x', 'y', 'z'};
        aLabelAdded = 0;
        bLabelAdded = 0;
        cLabelAdded = 0;

        for i = 1:3

            if round(aAxis.xyz, 10) == xyzVecs(i, :)
                aLabelAdded = 1;
                xyzLabels(i) = append(xyzLabels(i), '/a');
            end

            if round(bAxis.xyz, 10) == xyzVecs(i, :)
                bLabelAdded = 1;
                xyzLabels(i) = append(xyzLabels(i), '/b');
            end

            if round(cAxis.xyz, 10) == xyzVecs(i, :)
                cLabelAdded = 1;
                xyzLabels(i) = append(xyzLabels(i), '/c');
            end

        end

        if isfield(ori_data, 'orientation_coordinate_system')

            if isstruct(ori_data.orientation_coordinate_system)

                if isfield(ori_data.orientation_coordinate_system, 'x')
                    xyzLabels(1) = append( ...
                        xyzLabels(1), ...
                        sprintf('/%s', ori_data.orientation_coordinate_system.x) ...
                    );
                end

                if isfield(ori_data.orientation_coordinate_system, 'y')
                    xyzLabels(2) = append( ...
                        xyzLabels(2), ...
                        sprintf('/%s', ori_data.orientation_coordinate_system.y) ...
                    );
                end

                if isfield(ori_data.orientation_coordinate_system, 'z')
                    xyzLabels(3) = append( ...
                        xyzLabels(3), ...
                        sprintf('/%s', ori_data.orientation_coordinate_system.z) ...
                    );
                end

                annotate( ...
                    [xvector, yvector, zvector], ...
                    'label', { ...
                        ori_data.orientation_coordinate_system.x, ...
                        ori_data.orientation_coordinate_system.y, ...
                        ori_data.orientation_coordinate_system.z ...
                    }, ...
                    'backgroundcolor', 'w' ...
                )
            end

        end

        annotate( ...
            [xvector, yvector, zvector], ...
            'label', {xyzLabels{1}, xyzLabels{2}, xyzLabels{3}}, ...
            'backgroundcolor', 'w' ...
        )

        if ~aLabelAdded
            annotate([crystalSym.aAxis], 'label', {'a'}, 'backgroundcolor', 'w');
        end

        if ~bLabelAdded
            annotate([crystalSym.bAxis], 'label', {'b'}, 'backgroundcolor', 'w');
        end

        if ~cLabelAdded
            annotate([crystalSym.cAxis], 'label', {'c'}, 'backgroundcolor', 'w');
        end

        if isfield(ori_data, 'increment')
            fileName = sprintf('pole_figure_inc_%d.png', ori_data.increment);
        else
            fileName = 'pole_figure.png';
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
