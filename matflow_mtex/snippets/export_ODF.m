function exitcode = export_ODF(ODF, fileName)
    export(ODF, fileName, 'Bunge', 'MTEX');
    exitcode = 1;
end
