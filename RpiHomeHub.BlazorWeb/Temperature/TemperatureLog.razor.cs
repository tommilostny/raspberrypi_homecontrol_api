using Microsoft.AspNetCore.Components;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Temperature
{
    public partial class TemperatureLog : ComponentBase
    {
        [Inject]
        private HttpClient HttpClient { get; set; }

        private List<string> LogLines { get; set; }

        private async Task FetchLog()
        {
            LogLines = null;
            var response = await HttpClient.GetAsync("temp_log");
            var content = await response.Content.ReadAsStringAsync();
            LogLines = JsonConvert.DeserializeObject<List<string>>(content);
            LogLines.Reverse();
        }

        private async Task ClearLog()
        {
            var response = await HttpClient.DeleteAsync("temp_log");
            if (response.StatusCode == HttpStatusCode.OK)
            {
                LogLines = new List<string>();
            }
            //else ErrorDialog?
        }

        private int GetLinesCount() => LogLines is not null ? LogLines.Count : 0;

        protected override async Task OnInitializedAsync()
        {
            await FetchLog();
            await base.OnInitializedAsync();
        }
    }
}
