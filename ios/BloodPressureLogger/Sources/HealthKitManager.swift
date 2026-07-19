import Foundation
import HealthKit

/// Обгортка над HealthKit: запит дозволів і запис тиску + пульсу.
@MainActor
final class HealthKitManager: ObservableObject {
    private let store = HKHealthStore()

    /// Чи доступний HealthKit на цьому пристрої (на iPad/симуляторі може бути ні).
    @Published var isAvailable: Bool = HKHealthStore.isHealthDataAvailable()

    /// Останнє повідомлення про помилку для показу в UI (nil = все гаразд).
    @Published var lastError: String?

    // Типи даних, які ми записуємо.
    private let systolicType = HKQuantityType(.bloodPressureSystolic)
    private let diastolicType = HKQuantityType(.bloodPressureDiastolic)
    private let heartRateType = HKQuantityType(.heartRate)
    private let bloodPressureType = HKCorrelationType(.bloodPressure)

    private var typesToShare: Set<HKSampleType> {
        [systolicType, diastolicType, heartRateType, bloodPressureType]
    }

    /// Запитуємо дозвіл на запис. Health показує системний діалог лише раз.
    func requestAuthorization() async {
        guard HKHealthStore.isHealthDataAvailable() else {
            isAvailable = false
            return
        }
        do {
            try await store.requestAuthorization(toShare: typesToShare, read: [])
        } catch {
            lastError = "Не вдалося отримати дозвіл Health: \(error.localizedDescription)"
        }
    }

    /// Записує один вимір у Apple Health: кров'яний тиск (кореляція
    /// систолічний+діастолічний) і окремо пульс, усі з однаковою датою.
    /// Повертає true у разі успіху.
    func save(_ reading: Reading) async -> Bool {
        guard HKHealthStore.isHealthDataAvailable() else {
            lastError = "HealthKit недоступний на цьому пристрої."
            return false
        }

        let mmHg = HKUnit.millimeterOfMercury()
        let bpm = HKUnit.count().unitDivided(by: .minute())
        let date = reading.date

        let systolicSample = HKQuantitySample(
            type: systolicType,
            quantity: HKQuantity(unit: mmHg, doubleValue: Double(reading.systolic)),
            start: date, end: date
        )
        let diastolicSample = HKQuantitySample(
            type: diastolicType,
            quantity: HKQuantity(unit: mmHg, doubleValue: Double(reading.diastolic)),
            start: date, end: date
        )
        let bloodPressure = HKCorrelation(
            type: bloodPressureType,
            start: date, end: date,
            objects: [systolicSample, diastolicSample]
        )
        let heartRateSample = HKQuantitySample(
            type: heartRateType,
            quantity: HKQuantity(unit: bpm, doubleValue: Double(reading.pulse)),
            start: date, end: date
        )

        do {
            try await store.save([bloodPressure, heartRateSample])
            lastError = nil
            return true
        } catch {
            lastError = "Помилка запису в Health: \(error.localizedDescription)"
            return false
        }
    }
}
