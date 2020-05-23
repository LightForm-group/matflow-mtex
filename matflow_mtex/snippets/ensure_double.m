function doubleVal = ensure_double(doubleStr)
    if isa(doubleStr, 'double')
        doubleVal = doubleStr;
    else
        doubleVal = str2double(doubleStr);
    end
end
