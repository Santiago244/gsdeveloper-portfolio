%% RadioML AMC experiment visualization
% This script reads one experiment folder produced by src/train.py and
% src/evaluate.py, then creates thesis-style diagnostic plots.
%
% Default input:
%   experiments/cnn1d_quick_20260417_071055
%
% Output:
%   Detailed PNG figures saved into visualizations/by_model/<model>/
%   Presentation-ready PNG figures saved into
%   visualizations/by_model/<model>/presentation/

clear; clc; close all;
set(groot, "defaultFigureVisible", "off");

projectRoot = fileparts(fileparts(mfilename("fullpath")));
experimentFolders = [
    "cnn1d_baseline_20260511_180658-BS512"
    "cnn_lstm_baseline_20260512_062159-BS512"
    "resnet1d_baseline_20260513_004424-BS512"
];

for experimentIndex = 1:numel(experimentFolders)
experimentDir = fullfile(projectRoot, "experiments", experimentFolders(experimentIndex));
[~, experimentFolderName] = fileparts(experimentDir);
modelFolderName = folderToModelFolder(experimentFolderName);
outputDir = fullfile(projectRoot, "visualizations", "by_model", modelFolderName);
presentationDir = fullfile(outputDir, "presentation");

if ~exist(outputDir, "dir")
    mkdir(outputDir);
end
if ~exist(presentationDir, "dir")
    mkdir(presentationDir);
end

historyPath = fullfile(experimentDir, "history.csv");
trainReportPath = fullfile(experimentDir, "train_report.json");
testReportPath = fullfile(experimentDir, "test_report.json");
confusionPath = fullfile(experimentDir, "confusion_matrix.csv");

history = readtable(historyPath);
trainReport = readJsonFile(trainReportPath);
testReportText = fileread(testReportPath);
testReport = jsondecode(testReportText);
confusion = readmatrix(confusionPath);
modelDisplayName = formatModelName(string(testReport.model_type));

classNames = string(testReport.class_names);
if iscolumn(classNames)
    classNames = classNames;
end

metrics = computeMetricsFromConfusion(confusion);
[snrValues, snrAccuracy] = parseNumericJsonObject(testReportText, "per_snr_accuracy");

fprintf("Experiment: %s\n", string(testReport.experiment_name));
fprintf("Model type: %s\n", string(testReport.model_type));
fprintf("Test samples: %d\n", testReport.test_samples);
fprintf("Overall accuracy: %.2f %%\n", 100 * testReport.overall_accuracy);
fprintf("Macro precision: %.2f %%\n", 100 * testReport.macro_precision);
fprintf("Macro recall: %.2f %%\n", 100 * testReport.macro_recall);
fprintf("Macro F1: %.2f %%\n", 100 * testReport.macro_f1);
fprintf("Presentation figures:\n%s\n", presentationDir);

%% 1. Training and validation learning curves
fig = figure("Color", "w", "Position", [100, 100, 1100, 480]);
tiledlayout(1, 2, "Padding", "compact", "TileSpacing", "compact");

nexttile;
plot(history.epoch, history.train_loss, "-o", "LineWidth", 1.8, "MarkerSize", 5);
hold on;
plot(history.epoch, history.val_loss, "-s", "LineWidth", 1.8, "MarkerSize", 5);
grid on;
xlabel("Epoch");
ylabel("Cross-entropy loss");
title(modelDisplayName + ": Loss During Training");
legend(["Training", "Validation"], "Location", "northeast");
styleAxes(gca);

nexttile;
plot(history.epoch, 100 * history.train_accuracy, "-o", "LineWidth", 1.8, "MarkerSize", 5);
hold on;
plot(history.epoch, 100 * history.val_accuracy, "-s", "LineWidth", 1.8, "MarkerSize", 5);
grid on;
xlabel("Epoch");
ylabel("Accuracy (%)");
title(modelDisplayName + ": Accuracy During Training");
legend(["Training", "Validation"], "Location", "southeast");
ylim([0, 100]);
styleAxes(gca);

saveFigure(fig, outputDir, presentationDir, "01_learning_curves.png", true, 220);

%% 2. Summary metrics
summaryLabels = ["Accuracy", "Macro precision", "Macro recall", "Macro F1"];
summaryNames = categorical(summaryLabels, summaryLabels, "Ordinal", true);
summaryValues = 100 * [
    testReport.overall_accuracy;
    testReport.macro_precision;
    testReport.macro_recall;
    testReport.macro_f1
]';

fig = figure("Color", "w", "Position", [100, 100, 760, 460]);
bar(summaryNames, summaryValues, 0.65);
grid on;
ylabel("Score (%)");
ylim([0, max(100, ceil(max(summaryValues) / 10) * 10)]);
title(modelDisplayName + ": Test-Set Classification Metrics");
text(summaryNames, summaryValues + 1, compose("%.1f%%", summaryValues), ...
    "HorizontalAlignment", "center", "FontSize", 10);
styleAxes(gca);
saveFigure(fig, outputDir, presentationDir, "02_summary_metrics.png", true, 220);

%% 3. Accuracy versus SNR
fig = figure("Color", "w", "Position", [100, 100, 900, 500]);
plot(snrValues, 100 * snrAccuracy, "-o", "LineWidth", 2.0, "MarkerSize", 5);
grid on;
xlabel("SNR (dB)");
ylabel("Accuracy (%)");
title(modelDisplayName + ": Test Accuracy versus SNR");
xticks(snrValues);
ylim([0, 100]);
yline(100 / numel(classNames), "--", "Chance level", "LabelHorizontalAlignment", "left");
styleAxes(gca);
saveFigure(fig, outputDir, presentationDir, "03_accuracy_vs_snr.png", true, 220);

%% 4. Per-class precision, recall, F1, and accuracy
fig = figure("Color", "w", "Position", [100, 100, 1300, 620]);
tiledlayout(2, 1, "Padding", "compact", "TileSpacing", "compact");

nexttile;
bar(100 * [metrics.precision(:), metrics.recall(:), metrics.f1(:)]);
grid on;
ylabel("Score (%)");
title(modelDisplayName + ": Per-Class Precision, Recall, and F1");
legend(["Precision", "Recall", "F1"], "Location", "northeastoutside");
xticks(1:numel(classNames));
xticklabels(classNames);
xtickangle(45);
ylim([0, 100]);
styleAxes(gca);

nexttile;
bar(100 * metrics.accuracy, 0.75);
grid on;
ylabel("Accuracy (%)");
title(modelDisplayName + ": Per-Class Accuracy");
xticks(1:numel(classNames));
xticklabels(classNames);
xtickangle(45);
ylim([0, 100]);
styleAxes(gca);

saveFigure(fig, outputDir, presentationDir, "04_per_class_metrics.png", false, 220);

%% 5. Raw confusion matrix
fig = figure("Color", "w", "Position", [100, 100, 980, 860]);
imagesc(confusion);
axis image;
colormap(parula);
colorbar;
title(modelDisplayName + ": Confusion Matrix, Raw Counts");
xlabel("Predicted class");
ylabel("True class");
xticks(1:numel(classNames));
yticks(1:numel(classNames));
xticklabels(classNames);
yticklabels(classNames);
xtickangle(45);
styleAxes(gca);
saveFigure(fig, outputDir, presentationDir, "05_confusion_matrix_counts.png", false, 240);

%% 6. Row-normalized confusion matrix
rowTotals = sum(confusion, 2);
confusionNorm = confusion ./ max(rowTotals, 1);

fig = figure("Color", "w", "Position", [100, 100, 980, 860]);
imagesc(100 * confusionNorm);
axis image;
colormap(parula);
colorbar;
title(modelDisplayName + ": Confusion Matrix, Row-Normalized (%)");
xlabel("Predicted class");
ylabel("True class");
xticks(1:numel(classNames));
yticks(1:numel(classNames));
xticklabels(classNames);
yticklabels(classNames);
xtickangle(45);
styleAxes(gca);
saveFigure(fig, outputDir, presentationDir, "06_confusion_matrix_normalized.png", true, 240);

%% 7. Prediction bias diagnostic
trueCounts = sum(confusion, 2);
predictedCounts = sum(confusion, 1)';

fig = figure("Color", "w", "Position", [100, 100, 1300, 520]);
bar([trueCounts, predictedCounts]);
grid on;
ylabel("Number of samples");
title(modelDisplayName + ": True Class Distribution versus Predicted Distribution");
legend(["True labels", "Predicted labels"], "Location", "northeastoutside");
xticks(1:numel(classNames));
xticklabels(classNames);
xtickangle(45);
styleAxes(gca);
saveFigure(fig, outputDir, presentationDir, "07_prediction_bias.png", false, 220);

%% 8. SNR regime summary
snrGroups = [
    struct("name", "Low SNR (-20 to -10 dB)", "min", -20, "max", -10)
    struct("name", "Mid SNR (-8 to 6 dB)", "min", -8, "max", 6)
    struct("name", "High SNR (8 to 30 dB)", "min", 8, "max", 30)
];

groupNames = strings(numel(snrGroups), 1);
groupAcc = zeros(numel(snrGroups), 1);
for i = 1:numel(snrGroups)
    mask = snrValues >= snrGroups(i).min & snrValues <= snrGroups(i).max;
    groupNames(i) = snrGroups(i).name;
    groupAcc(i) = mean(snrAccuracy(mask));
end

fig = figure("Color", "w", "Position", [100, 100, 850, 460]);
groupCat = categorical(groupNames, groupNames, "Ordinal", true);
bar(groupCat, 100 * groupAcc, 0.6);
grid on;
ylabel("Mean accuracy across SNR values (%)");
title(modelDisplayName + ": Accuracy by SNR Regime");
ylim([0, 100]);
text(groupCat, 100 * groupAcc + 1, compose("%.1f%%", 100 * groupAcc), ...
    "HorizontalAlignment", "center", "FontSize", 10);
styleAxes(gca);
saveFigure(fig, outputDir, presentationDir, "08_snr_regime_accuracy.png", true, 220);

fprintf("Saved figures to:\n%s\n", outputDir);
fprintf("Saved selected presentation figures to:\n%s\n", presentationDir);
close all;
end

%% Local helper functions
function data = readJsonFile(path)
    text = fileread(path);
    data = jsondecode(text);
end

function modelFolderName = folderToModelFolder(experimentFolderName)
    experimentFolderName = lower(string(experimentFolderName));
    if contains(experimentFolderName, "cnn_lstm")
        modelFolderName = "cnn_lstm";
    elseif contains(experimentFolderName, "cnn1d")
        modelFolderName = "cnn1d";
    elseif contains(experimentFolderName, "resnet1d")
        modelFolderName = "resnet1d";
    else
        modelFolderName = experimentFolderName;
    end
end

function name = formatModelName(modelType)
    switch lower(string(modelType))
        case "cnn1d"
            name = "CNN1D";
        case "cnn_lstm"
            name = "CNN-LSTM";
        case "resnet1d"
            name = "ResNet1D";
        otherwise
            name = string(modelType);
    end
end

function saveFigure(fig, outputDir, presentationDir, filename, includeInPresentation, resolution)
    exportgraphics(fig, fullfile(outputDir, filename), "Resolution", resolution);
    if includeInPresentation
        exportgraphics(fig, fullfile(presentationDir, filename), "Resolution", resolution);
    end
end

function styleAxes(ax)
    ax.FontSize = 11;
    ax.LineWidth = 0.9;
    ax.Box = "on";
    grid(ax, "on");
end

function metrics = computeMetricsFromConfusion(confusion)
    tp = diag(confusion);
    predictedTotal = sum(confusion, 1)';
    actualTotal = sum(confusion, 2);

    precision = safeDivide(tp, predictedTotal);
    recall = safeDivide(tp, actualTotal);
    f1 = safeDivide(2 * precision .* recall, precision + recall);
    accuracy = recall;

    metrics = struct();
    metrics.precision = precision;
    metrics.recall = recall;
    metrics.f1 = f1;
    metrics.accuracy = accuracy;
end

function out = safeDivide(num, den)
    out = zeros(size(num));
    mask = den > 0;
    out(mask) = num(mask) ./ den(mask);
end

function [keys, values] = parseNumericJsonObject(jsonText, objectName)
    pattern = """" + objectName + """\s*:\s*\{(?<body>.*?)\}";
    match = regexp(jsonText, pattern, "names", "once");
    if isempty(match)
        error("Could not find JSON object named %s.", objectName);
    end

    pairPattern = """(?<key>-?\d+)""\s*:\s*(?<value>[-+0-9.eE]+)";
    pairs = regexp(match.body, pairPattern, "names");
    keys = zeros(numel(pairs), 1);
    values = zeros(numel(pairs), 1);

    for i = 1:numel(pairs)
        keys(i) = str2double(pairs(i).key);
        values(i) = str2double(pairs(i).value);
    end

    [keys, order] = sort(keys);
    values = values(order);
end
