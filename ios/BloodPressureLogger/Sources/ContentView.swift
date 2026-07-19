import SwiftUI
import UIKit

struct ContentView: View {
    @EnvironmentObject private var store: ReadingStore
    @EnvironmentObject private var health: HealthKitManager

    // Поля форми. Тримаємо як текст, щоб зручно було вводити з клавіатури.
    @State private var systolic = ""
    @State private var diastolic = ""
    @State private var pulse = ""
    @State private var banner: String?
    @State private var showCamera = false
    @State private var isRecognizing = false

    var body: some View {
        NavigationStack {
            Form {
                inputSection
                historySection
            }
            .navigationTitle("Тиск")
            .safeAreaInset(edge: .bottom) { bannerView }
            .fullScreenCover(isPresented: $showCamera) {
                CameraPicker { image in
                    showCamera = false
                    Task { await recognize(from: image) }
                }
                .ignoresSafeArea()
            }
        }
    }

    // MARK: - Форма вводу

    private var inputSection: some View {
        Section("Новий вимір") {
            Button {
                showCamera = true
            } label: {
                Label(
                    isRecognizing ? "Розпізнаю…" : "Сфотографувати показники",
                    systemImage: isRecognizing ? "hourglass" : "camera.fill"
                )
                .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)
            .disabled(isRecognizing)

            field(title: "Систолічний (SYS)", text: $systolic, unit: "mmHg")
            field(title: "Діастолічний (DIA)", text: $diastolic, unit: "mmHg")
            field(title: "Пульс (PUL)", text: $pulse, unit: "уд/хв")

            Button {
                Task { await saveReading() }
            } label: {
                Label("Зберегти", systemImage: "square.and.arrow.down")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.borderedProminent)
            .disabled(!isValid)
        }
    }

    private func field(title: String, text: Binding<String>, unit: String) -> some View {
        HStack {
            Text(title)
            Spacer()
            TextField("0", text: text)
                .keyboardType(.numberPad)
                .multilineTextAlignment(.trailing)
                .frame(width: 70)
            Text(unit).foregroundStyle(.secondary)
        }
    }

    // MARK: - Історія

    private var historySection: some View {
        Section("Історія") {
            if store.readings.isEmpty {
                Text("Ще немає вимірів").foregroundStyle(.secondary)
            } else {
                ForEach(store.readings) { reading in
                    ReadingRow(reading: reading)
                }
                .onDelete { store.delete(at: $0) }
            }
        }
    }

    // MARK: - Банер статусу

    @ViewBuilder private var bannerView: some View {
        if let banner {
            Text(banner)
                .font(.footnote)
                .padding(10)
                .frame(maxWidth: .infinity)
                .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 10))
                .padding(.horizontal)
        }
    }

    // MARK: - Логіка

    private var isValid: Bool {
        [systolic, diastolic, pulse].allSatisfy { Int($0) != nil && !$0.isEmpty }
    }

    /// Розпізнає числа з фото і підставляє їх у форму (без авто-збереження).
    /// Саме фото ніде не зберігається — після цього виклику воно зникає.
    private func recognize(from image: UIImage?) async {
        guard let image else { return } // користувач скасував зйомку
        isRecognizing = true
        let result = await TextRecognizer.recognize(from: image)
        isRecognizing = false

        if let sys = result.systolic { systolic = String(sys) }
        if let dia = result.diastolic { diastolic = String(dia) }
        if let pul = result.pulse { pulse = String(pul) }

        let found = [result.systolic, result.diastolic, result.pulse].compactMap { $0 }.count
        banner = found == 3
            ? "Розпізнано з фото — перевір значення і натисни «Зберегти». Фото не збережено."
            : "Розпізнав частково (\(found)/3). Заповни решту вручну. Фото не збережено."

        try? await Task.sleep(nanoseconds: 4_000_000_000)
        banner = nil
    }

    private func saveReading() async {
        guard let sys = Int(systolic), let dia = Int(diastolic), let pul = Int(pulse) else { return }

        var reading = Reading(systolic: sys, diastolic: dia, pulse: pul, date: Date())

        // 1) Пишемо в Apple Health.
        let ok = await health.save(reading)
        reading.savedToHealth = ok

        // 2) Додаємо в локальну історію (з теперішнім часом і датою).
        store.add(reading)

        // 3) Очищаємо форму й показуємо результат.
        systolic = ""; diastolic = ""; pulse = ""
        banner = ok
            ? "Збережено \(sys)/\(dia), пульс \(pul) — і в Health ✔"
            : (health.lastError ?? "Збережено локально, але не в Health")

        try? await Task.sleep(nanoseconds: 3_000_000_000)
        banner = nil
    }
}

// MARK: - Рядок історії

private struct ReadingRow: View {
    let reading: Reading

    private static let dateFormatter: DateFormatter = {
        let f = DateFormatter()
        f.locale = Locale(identifier: "uk_UA")
        f.dateFormat = "d MMM yyyy, HH:mm"
        return f
    }()

    var body: some View {
        HStack(spacing: 12) {
            Circle()
                .fill(color(for: reading.category))
                .frame(width: 10, height: 10)

            VStack(alignment: .leading, spacing: 2) {
                Text("\(reading.systolic)/\(reading.diastolic) mmHg  ·  \(reading.pulse) уд/хв")
                    .font(.body.monospacedDigit())
                Text("\(Self.dateFormatter.string(from: reading.date))  ·  \(reading.category.rawValue)")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            Image(systemName: reading.savedToHealth ? "heart.fill" : "heart.slash")
                .foregroundStyle(reading.savedToHealth ? .pink : .secondary)
                .font(.caption)
        }
        .padding(.vertical, 2)
    }

    private func color(for category: Reading.Category) -> Color {
        switch category.tintName {
        case "blue": return .blue
        case "green": return .green
        case "yellow": return .yellow
        case "orange": return .orange
        case "red": return .red
        case "purple": return .purple
        default: return .gray
        }
    }
}

#Preview {
    ContentView()
        .environmentObject(ReadingStore())
        .environmentObject(HealthKitManager())
}
