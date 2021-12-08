function ODF = get_model_ODF(ODFComponentDefnsJSONPath, crystalSym, specimenSym)

    crystalSym = crystalSymmetry(crystalSym);
    specimenSym = specimenSymmetry(specimenSym);

    % Note, for this to work in a consistent way, the objects in the array
    % of ODF component should each have a distinct key. Otherwise,
    % `jsondecode` will load the array into a structure array.
    ODFComponentsDefns = jsondecode(fileread(ODFComponentDefnsJSONPath));

    % Normalise `jsondecode`'s "helpful" parsing in the case where there
    % is just one object in the array of ODF components:
    if isstruct(ODFComponentsDefns)
        ODFComponentsDefns = {ODFComponentsDefns};
    end

    for i = 1:length(ODFComponentsDefns)

        comp = ODFComponentsDefns{i};

        if strcmp(comp.type, 'unimodal')
            kernel = deLaValleePoussinKernel( ...
                'halfwidth', ...
                comp.halfwidth * degree ...
            );

            if isfield(comp, 'modalOrientationHKL')
                modalOri = orientation.byMiller( ...
                    comp.modalOrientationHKL.', ...
                    comp.modalOrientationUVW.', ...
                    crystalSym, ...
                    specimenSym ...
                );

            elseif isfield(comp, 'modalOrientationEuler')
                euler_deg = num2cell(comp.modalOrientationEuler * degree);
                modalOri = orientation.byEuler(euler_deg{:}, crystalSym, specimenSym);

            end

            ODFComponent = unimodalODF(modalOri, kernel);

        elseif strcmp(comp.type, 'uniform')
            ODFComponent = uniformODF(crystalSym, specimenSym);

        elseif strcmp(comp.type, 'fibre')
            kernel = deLaValleePoussinKernel( ...
                'halfwidth', ...
                comp.halfwidth * degree ...
            );

            if isfield(comp, 'mtexfibre')

                if strcmp(comp.mtexfibre, 'alpha')
                    ODFComponent = fibreODF(fibre.alpha(crystalSym, specimenSym), kernel);

                elseif strcmp(comp.mtexfibre, 'beta')
                    ODFComponent = fibreODF(fibre.beta(crystalSym, specimenSym), kernel);

                elseif strcmp(comp.mtexfibre, 'epsilon')
                    ODFComponent = fibreODF(fibre.epsilon(crystalSym, specimenSym), kernel);

                elseif strcmp(comp.mtexfibre, 'eta')
                    ODFComponent = fibreODF(fibre.eta(crystalSym, specimenSym), kernel);

                elseif strcmp(comp.mtexfibre, 'fit')
                    ODFComponent = fibreODF(fibre.fit(crystalSym, specimenSym), kernel);

                elseif strcmp(comp.mtexfibre, 'gamma')
                    ODFComponent = fibreODF(fibre.gamma(crystalSym, specimenSym), kernel);

                elseif strcmp(comp.mtexfibre, 'rand')
                    ODFComponent = fibreODF(fibre.rand(crystalSym, specimenSym), kernel);

                elseif strcmp(comp.mtexfibre, 'tau')
                    ODFComponent = fibreODF(fibre.tau(crystalSym, specimenSym), kernel);
                end

            elseif isfield(comp, 'fibreCrystalDir')

                fibreCrystalDir = num2cell(comp.fibreCrystalDir)
                f = fibre( ...
                    Miller(fibreCrystalDir{:}, crystalSym), ...
                    vector3d.(upper(comp.fibreSpecimenDir)) ...
                )
                ODFComponent = fibreODF(f, kernel)

            end

        end

        if i == 1
            ODF = comp.componentFraction * ODFComponent;
        else
            ODF = ODF + (comp.componentFraction * ODFComponent);
        end

    end

end
