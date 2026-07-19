import Foundation

/// Формує CSV-файл з історії вимірів для експорту (напр. показати лікарю).
enum CSVExporter {

    private static let dateFormatter: DateFormatter = {
        let f = DateFormatter()
        f.locale = Locale(identifier: "uk_UA")
        f.dateFormat = "yyyy-MM-dd HH:mm"
        return f
    }()

    /// Створює тимчасовий CSV-файл і повертає його URL для аркуша «Поділитися».
    static func makeFile(from readings: [Reading]) -> URL? {
        var rows = ["Дата,Систолічний,Діастолічний,Пульс,Категорія"]
        for reading in readings.sorted(by: { $0.date < $1.date }) {
            let line = "\(dateFormatter.string(from: reading.date)),"
                + "\(reading.systolic),\(reading.diastolic),\(reading.pulse),"
                + "\(reading.category.rawValue)"
            rows.append(line)
        }

        // BOM, щоб Excel коректно показував кирилицю у UTF-8.
        let csv = "\u{FEFF}" + rows.joined(separator: "\n")
        let url = FileManager.default.temporaryDirectory
            .appendingPathComponent("Тиск-історія.csv")

        do {
            try csv.data(using: .utf8)?.write(to: url, options: [.atomic])
            return url
        } catch {
            return nil
        }
    }
}
