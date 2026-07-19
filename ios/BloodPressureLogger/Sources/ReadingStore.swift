import Foundation

/// Локальне сховище історії вимірів.
/// Зберігає масив у JSON-файлі в теці Application Support, тож дані
/// не зникають між запусками застосунку.
@MainActor
final class ReadingStore: ObservableObject {
    @Published private(set) var readings: [Reading] = []

    private let fileURL: URL

    init() {
        let dir = FileManager.default
            .urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
        try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
        self.fileURL = dir.appendingPathComponent("readings.json")
        load()
    }

    /// Додає вимір і одразу зберігає на диск. Найновіші — зверху.
    func add(_ reading: Reading) {
        readings.insert(reading, at: 0)
        readings.sort { $0.date > $1.date }
        persist()
    }

    /// Позначає вимір як записаний у Health (після успішного запису).
    func markSavedToHealth(_ id: UUID) {
        guard let idx = readings.firstIndex(where: { $0.id == id }) else { return }
        readings[idx].savedToHealth = true
        persist()
    }

    func delete(at offsets: IndexSet) {
        readings.remove(atOffsets: offsets)
        persist()
    }

    // MARK: - Persistence

    private func load() {
        guard let data = try? Data(contentsOf: fileURL) else { return }
        if let decoded = try? JSONDecoder().decode([Reading].self, from: data) {
            readings = decoded.sorted { $0.date > $1.date }
        }
    }

    private func persist() {
        guard let data = try? JSONEncoder().encode(readings) else { return }
        try? data.write(to: fileURL, options: [.atomic])
    }
}
