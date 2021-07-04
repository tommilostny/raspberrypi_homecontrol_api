using System;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Microsoft.Extensions.DependencyInjection;
using RpiHomeHub.BlazorWeb.LCD;
using RpiHomeHub.BlazorWeb.Colors.Services;
using RpiHomeHub.BlazorWeb.Lights.Services;

namespace RpiHomeHub.BlazorWeb
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = WebAssemblyHostBuilder.CreateDefault(args);
            builder.RootComponents.Add<App>("#app");

            builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri("http://192.168.1.242:5000/") });

            builder.Services.AddScoped<YeelightService>();
            builder.Services.AddScoped<LampService>();
            builder.Services.AddScoped<LED_StripService>();
            builder.Services.AddScoped<AllLightsService>();

            builder.Services.AddScoped<ColorDbService>();

            builder.Services.AddTransient<LCD_Service>();

            await builder.Build().RunAsync();
        }
    }
}
