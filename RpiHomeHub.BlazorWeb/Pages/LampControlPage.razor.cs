﻿using Microsoft.AspNetCore.Components;
using RpiHomeHub.BlazorWeb.Lights.Services;
using RpiHomeHub.BlazorWeb.Lights.Models;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Pages
{
    public partial class LampControlPage : ComponentBase
    {
        [Inject]
        public LampService LampService { get; set; }

        private LampModel Lamp { get; set; }

        protected override async Task OnInitializedAsync()
        {
            await Load();
            await base.OnInitializedAsync();
        }

        private async Task Load()
        {
            Lamp = await LampService.GetStatusAsync();
        }
    }
}
