function ODF = load_ODF(ODF_path, crystalSym, specimenSym)
    crystalSym = crystalSymmetry(crystalSym);
    specimenSym = specimenSymmetry(specimenSym);    
    ODF = loadODF_generic(ODF_path, 'cs', crystalSym, 'ss', specimenSym,...
        'ColumnNames',{'Euler 1' 'Euler 2' 'Euler 3' 'weight'}...
    );
end
