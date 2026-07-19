import SwiftUI

@main
struct BloodPressureLoggerApp: App {
    // Спільне сховище історії та менеджер HealthKit на весь застосунок.
    @StateObject private var store = ReadingStore()
    @StateObject private var health = HealthKitManager()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(store)
                .environmentObject(health)
                .task {
                    // Просимо дозвіл на запис у Health одразу при старті.
                    await health.requestAuthorization()
                }
        }
    }
}
