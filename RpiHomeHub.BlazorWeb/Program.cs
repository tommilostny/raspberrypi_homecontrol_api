using System;
using System.Net.Http;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Text;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using RpiHomeHub.BlazorWeb.Services;

namespace RpiHomeHub.BlazorWeb
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = WebAssemblyHostBuilder.CreateDefault(args);
            builder.RootComponents.Add<App>("#app");

            builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri("http://192.168.1.242:5000/") });
            builder.Services.AddScoped<YeelightBulbService>();
            builder.Services.AddTransient<LCD_Service>();

            await builder.Build().RunAsync();
        }
    }
}
