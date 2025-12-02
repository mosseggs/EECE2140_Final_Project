function truth_table_ui_ipina()
% MATLAB UI for interacting with truth_table_ipina_extended.py

    hFig = figure('Name','Truth Table Utility','NumberTitle','off',...
        'MenuBar','none','ToolBar','none','Position',[300 300 700 500]);

    uicontrol('Parent',hFig,'Style','text','String','Truth Table Utility',...
        'FontSize',14,'FontWeight','bold','HorizontalAlignment','center',...
        'Units','normalized','Position',[0.05 0.92 0.9 0.06]);

    homePanel = uipanel('Parent',hFig,'Title','Home','Units','normalized',...
        'Position',[0.02 0.6 0.96 0.3]);

    uicontrol('Parent',homePanel,'Style','pushbutton','String','Input Boolean Expression',...
        'Units','normalized','Position',[0.05 0.15 0.4 0.6],'FontSize',12,'Callback',@onExpr);

    uicontrol('Parent',homePanel,'Style','pushbutton','String','Input Truth Table',...
        'Units','normalized','Position',[0.55 0.15 0.4 0.6],'FontSize',12,'Callback',@onManual);

    uicontrol('Parent',hFig,'Style','text','String','Output','Units','normalized',...
        'Position',[0.02 0.55 0.1 0.03],'HorizontalAlignment','left');

    outputBox = uicontrol('Parent',hFig,'Style','edit','Max',2,'Min',0,...
        'Units','normalized','HorizontalAlignment','left','Enable','inactive',...
        'FontName','FixedWidth','Position',[0.02 0.05 0.96 0.5]);

    uicontrol('Parent',hFig,'Style','text','String',...
        'Note: Python must be on PATH. truth_table_ipina_extended.py must be in this folder.',...
        'Units','normalized','Position',[0.02 0.01 0.96 0.03],...
        'HorizontalAlignment','left','FontSize',9);


    %  Boolean Expression Mode
    function onExpr(~,~)
        a = inputdlg({'Enter boolean expression:'}, ...
            'Expression', [1 80], {''});
        if isempty(a), return; end

        expr = string(a{1});
        expr = strrep(expr,'"','\"');

        cmd = sprintf('python "%s" expr "%s"', ...
            fullfile(pwd,'truth_table_ipina_extended.py'), expr);

        [status,cmdout] = system(cmd);
        if status ~= 0
            cmdout = sprintf('Error running python script:\n%s',cmdout);
        end

        set(outputBox,'String',cmdout);
    end



    %  Manual Truth Table Mode
    function onManual(~,~)
        a = inputdlg({'Enter number of variables (2..5):'}, ...
            'Variables', [1 30], {'3'});
        if isempty(a), return; end

        n = str2double(a{1});
        if isnan(n) || n < 2 || n > 5
            errordlg('Number of variables must be 2–5.');
            return;
        end

        required = 2^n;
        def = strjoin(repmat({'0'},required,1), newline);

        outdlg = inputdlg( ...
            {sprintf('Enter %d outputs (0/1), one per line:', required)}, ...
            'Outputs', [20 80], {def});
        if isempty(outdlg), return; end


        outs_raw = outdlg{1};

        % Convert to string array
        outs_raw = string(outs_raw);
        outs_raw = join(outs_raw, newline);
        outs_raw = outs_raw(1);  

        outs_lines = splitlines(outs_raw);

        outs_lines = strtrim(outs_lines);
        outs_lines = outs_lines(outs_lines ~= "");

        if numel(outs_lines) == 1
            row1 = outs_lines(1);
            if contains(row1, ',')
                outs_lines = string(strsplit(row1, ','));
            elseif contains(row1, ' ')
                outs_lines = string(strsplit(row1, ' '));
            end
        end

        outs_lines = strtrim(outs_lines);
        outs_lines = outs_lines(outs_lines ~= "");

        outs = outs_lines( outs_lines == "0" | outs_lines == "1" );

        if numel(outs) ~= required
            errordlg(sprintf( ...
                'You must enter exactly %d valid values. You entered %d.', ...
                required, numel(outs)));
            return;
        end


        tmpfile = fullfile(pwd, sprintf('tt_tmp_%d.txt', round(now*1e6)));
        fid = fopen(tmpfile,'w');
        for i = 1:required
            fprintf(fid,"%s\n", outs(i));
        end
        fclose(fid);


        %% Run python
        cmd = sprintf('python "%s" manual %d "%s"', ...
            fullfile(pwd,'truth_table_ipina_extended.py'), n, tmpfile);

        [status,cmdout] = system(cmd);
        try, delete(tmpfile); end

        if status ~= 0
            cmdout = sprintf('Error running python script:\n%s',cmdout);
        end

        set(outputBox,'String',cmdout);
    end

end
