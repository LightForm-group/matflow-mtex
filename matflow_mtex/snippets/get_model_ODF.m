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
            
        elseif strcmp(ODFComponentsDefns{i}.type, 'fibre')        
            kernel = deLaValleePoussinKernel(...
                'halfwidth',...
                comp.halfwidth*degree...
            );
            if strcmp(ODFComponentsDefns{i}.mtexfibre, 'alpha')
                ODFComponent = fibreODF(fibre.alpha(crystalSym,specimenSym),kernel);
                
            elseif strcmp(ODFComponentsDefns{i}.mtexfibre, 'beta')
                ODFComponent = fibreODF(fibre.beta(crystalSym,specimenSym),kernel);
                
            elseif strcmp(ODFComponentsDefns{i}.mtexfibre, 'epsilon')
                ODFComponent = fibreODF(fibre.epsilon(crystalSym,specimenSym),kernel); 
                
            elseif strcmp(ODFComponentsDefns{i}.mtexfibre, 'eta')
                ODFComponent = fibreODF(fibre.eta(crystalSym,specimenSym),kernel);
                
            elseif strcmp(ODFComponentsDefns{i}.mtexfibre, 'fit')
                ODFComponent = fibreODF(fibre.fit(crystalSym,specimenSym),kernel);
                
            elseif strcmp(ODFComponentsDefns{i}.mtexfibre, 'gamma')
                ODFComponent = fibreODF(fibre.gamma(crystalSym,specimenSym),kernel);
                
            elseif strcmp(ODFComponentsDefns{i}.mtexfibre, 'rand')
                ODFComponent = fibreODF(fibre.rand(crystalSym,specimenSym),kernel); 
                
            elseif strcmp(ODFComponentsDefns{i}.mtexfibre, 'tau')
                ODFComponent = fibreODF(fibre.tau(crystalSym,specimenSym),kernel); 
            end
            
        end
                       
        if i == 1
            ODF = comp.componentFraction * ODFComponent;
        else
            ODF = ODF + (comp.componentFraction * ODFComponent);
        end
        
    end
    
end
