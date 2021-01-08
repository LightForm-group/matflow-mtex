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
            kernel = deLaValleePoussinKernel(...
                'halfwidth',...
                comp.halfwidth*degree...
            );
            modalOri = orientation.byMiller(...
                comp.modalOrientationHKL.',...
                comp.modalOrientationUVW.',...
                crystalSym,...
                specimenSym...
            );
            ODFComponent = unimodalODF(modalOri, kernel);
            
        elseif strcmp(ODFComponentsDefns{i}.type, 'uniform')
            ODFComponent = uniformODF(crystalSym, specimenSym);
            
        end
                       
        if i == 1
            ODF = comp.componentFraction * ODFComponent;
        else
            ODF = ODF + (comp.componentFraction * ODFComponent);
        end
        
    end
    
end
